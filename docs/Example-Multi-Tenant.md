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
﻿## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 572s 
    Code: 1771155095
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
    disk:97594
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771155095
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-1-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97594
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771155095
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-2-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97594
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771155095
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-2-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97594
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771155095
        TENANT_BY:schema
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-2-1  PostgreSQL-BHT-2-2-2
Pricing Summary Report (TPC-H Q1)                                 2411.08               2403.19               2425.79               2407.37
Minimum Cost Supplier Query (TPC-H Q2)                             439.94                467.01                434.89                414.78
Shipping Priority (TPC-H Q3)                                       697.77                707.71                666.93                668.20
Order Priority Checking Query (TPC-H Q4)                           351.26                350.15                341.89                333.54
Local Supplier Volume (TPC-H Q5)                                   616.96                625.09                618.80                598.31
Forecasting Revenue Change (TPC-H Q6)                              444.14                462.67                452.13                443.85
Forecasting Revenue Change (TPC-H Q7)                              689.42                727.88                735.41                693.86
National Market Share (TPC-H Q8)                                   404.82                405.47                378.89                359.16
Product Type Profit Measure (TPC-H Q9)                             957.99                984.81                967.66                943.49
Forecasting Revenue Change (TPC-H Q10)                             591.24                593.20                592.22                589.27
Important Stock Identification (TPC-H Q11)                         176.00                159.46                159.83                148.27
Shipping Modes and Order Priority (TPC-H Q12)                      657.38                641.41                652.67                635.84
Customer Distribution (TPC-H Q13)                                 2173.49               2106.22               2102.04               2111.43
Forecasting Revenue Change (TPC-H Q14)                             813.81                485.70                804.44                483.60
Top Supplier Query (TPC-H Q15)                                     527.44                495.87                502.02                494.56
Parts/Supplier Relationship (TPC-H Q16)                            547.92                558.22                544.22                553.96
Small-Quantity-Order Revenue (TPC-H Q17)                          2083.41               2032.64               1980.89               1857.56
Large Volume Customer (TPC-H Q18)                                 5590.37               5483.93               5752.63               5201.23
Discounted Revenue (TPC-H Q19)                                     120.62                447.17                120.57                112.69
Potential Part Promotion (TPC-H Q20)                               288.97                265.12                257.49                232.03
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                747.58                736.89                732.50                739.62
Global Sales Opportunity Query (TPC-H Q22)                         214.11                286.57                213.69                210.73

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-2-1-1           1.0          129.0         2.0      227.0     360.0
PostgreSQL-BHT-2-1-2           1.0          129.0         2.0      227.0     360.0
PostgreSQL-BHT-2-2-1           1.0          129.0         2.0      227.0     360.0
PostgreSQL-BHT-2-2-2           1.0          129.0         2.0      227.0     360.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-2-1-1           0.63
PostgreSQL-BHT-2-1-2           0.66
PostgreSQL-BHT-2-2-1           0.62
PostgreSQL-BHT-2-2-2           0.59

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-2-1-1            5684.00
PostgreSQL-BHT-2-1-2            5443.38
PostgreSQL-BHT-2-2-1            5791.32
PostgreSQL-BHT-2-2-2            6120.36

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-2-1 1.0 1              1                 23      2  1.0          6886.96
PostgreSQL-BHT-2-2 1.0 1              2                 23      2  1.0          6886.96

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1  1.0     2               1           1       1771155499     1771155522
PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-1  1.0     2               1           1       1771155499     1771155522
PostgreSQL-BHT-2-2-1  PostgreSQL-BHT-2-2  1.0     2               1           2       1771155589     1771155612
PostgreSQL-BHT-2-2-2  PostgreSQL-BHT-2-2  1.0     2               1           2       1771155589     1771155611

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
﻿## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 610s 
    Code: 1771155700
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
    disk:97594
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771155700
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-2-1-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97594
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771155700
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-2-2-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97594
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771155700
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-2-2-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97594
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771155700
        TENANT_BY:database
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-2-1  PostgreSQL-BHT-2-2-2
Pricing Summary Report (TPC-H Q1)                                 2339.14               2339.15               2354.55               2333.40
Minimum Cost Supplier Query (TPC-H Q2)                             475.97                475.18                448.23                435.29
Shipping Priority (TPC-H Q3)                                       729.15                722.66                680.85                676.14
Order Priority Checking Query (TPC-H Q4)                           345.44                358.37                334.99                339.41
Local Supplier Volume (TPC-H Q5)                                   635.65                650.81                603.69                598.11
Forecasting Revenue Change (TPC-H Q6)                              458.58                459.99                457.22                462.24
Forecasting Revenue Change (TPC-H Q7)                              733.81                737.84                740.04                725.54
National Market Share (TPC-H Q8)                                   401.07                410.26                361.17                358.89
Product Type Profit Measure (TPC-H Q9)                            1030.49               1067.78               1008.55               1043.03
Forecasting Revenue Change (TPC-H Q10)                             599.43                605.27                592.52                596.91
Important Stock Identification (TPC-H Q11)                         173.38                175.99                163.08                163.00
Shipping Modes and Order Priority (TPC-H Q12)                      651.43                644.70                638.43                642.80
Customer Distribution (TPC-H Q13)                                 2194.86               2181.35               2168.06               2141.28
Forecasting Revenue Change (TPC-H Q14)                             790.36                501.27                799.17                490.90
Top Supplier Query (TPC-H Q15)                                     499.11                509.16                533.64                501.28
Parts/Supplier Relationship (TPC-H Q16)                            572.82                573.23                569.70                572.44
Small-Quantity-Order Revenue (TPC-H Q17)                          2059.72               2100.73               2023.26               2003.95
Large Volume Customer (TPC-H Q18)                                 6730.98               6925.01               5450.66               5665.36
Discounted Revenue (TPC-H Q19)                                     119.97                131.79                116.98                115.29
Potential Part Promotion (TPC-H Q20)                               268.47                279.74                266.30                232.16
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                764.56                756.26                758.91                756.73
Global Sales Opportunity Query (TPC-H Q22)                         216.91                220.10                216.33                217.89

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-2-1-1           1.0          125.0         3.0      228.0     359.0
PostgreSQL-BHT-2-1-2           1.0          125.0         3.0      228.0     359.0
PostgreSQL-BHT-2-2-1           1.0          125.0         3.0      228.0     359.0
PostgreSQL-BHT-2-2-2           1.0          125.0         3.0      228.0     359.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-2-1-1           0.64
PostgreSQL-BHT-2-1-2           0.64
PostgreSQL-BHT-2-2-1           0.63
PostgreSQL-BHT-2-2-2           0.61

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-2-1-1            5593.32
PostgreSQL-BHT-2-1-2            5624.76
PostgreSQL-BHT-2-2-1            5755.89
PostgreSQL-BHT-2-2-2            5937.99

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-2-1 1.0 1              1                 24      2  1.0           6600.0
PostgreSQL-BHT-2-2 1.0 1              2                 25      2  1.0           6336.0

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1  1.0     2               1           1       1771156140     1771156164
PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-1  1.0     2               1           1       1771156140     1771156164
PostgreSQL-BHT-2-2-1  PostgreSQL-BHT-2-2  1.0     2               1           2       1771156233     1771156257
PostgreSQL-BHT-2-2-2  PostgreSQL-BHT-2-2  1.0     2               1           2       1771156232     1771156256

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
﻿## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 593s 
    Code: 1771156339
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
    disk:97595
    volume_size:5.0G
    volume_used:2.7G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771156339
        TENANT_BY:container
        TENANT_NUM:2
PostgreSQL-BHT-1-0-2-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97595
    volume_size:5.0G
    volume_used:2.7G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771156339
        TENANT_BY:container
        TENANT_NUM:2
PostgreSQL-BHT-1-1-1-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97595
    volume_size:5.0G
    volume_used:2.7G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771156339
        TENANT_BY:container
        TENANT_NUM:2
        TENANT:1
PostgreSQL-BHT-1-1-2-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97595
    volume_size:5.0G
    volume_used:2.7G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771156339
        TENANT_BY:container
        TENANT_NUM:2
        TENANT:1

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-1-0-1-1  PostgreSQL-BHT-1-0-2-1  PostgreSQL-BHT-1-1-1-1  PostgreSQL-BHT-1-1-2-1
Pricing Summary Report (TPC-H Q1)                                   2323.83                 2323.94                 2290.83                 2291.34
Minimum Cost Supplier Query (TPC-H Q2)                               442.91                  411.17                  437.90                  431.78
Shipping Priority (TPC-H Q3)                                         694.18                  639.91                  707.41                  654.76
Order Priority Checking Query (TPC-H Q4)                             333.77                  324.71                  342.06                  330.32
Local Supplier Volume (TPC-H Q5)                                     613.14                  586.61                  613.64                  606.73
Forecasting Revenue Change (TPC-H Q6)                                458.29                  459.37                  463.16                  465.34
Forecasting Revenue Change (TPC-H Q7)                                693.12                  675.17                  687.50                  717.34
National Market Share (TPC-H Q8)                                     407.95                  374.46                  400.86                  380.60
Product Type Profit Measure (TPC-H Q9)                              1039.37                 1015.17                  988.76                  985.89
Forecasting Revenue Change (TPC-H Q10)                               577.13                  569.43                  590.58                  595.99
Important Stock Identification (TPC-H Q11)                           177.85                  161.73                  161.25                  171.17
Shipping Modes and Order Priority (TPC-H Q12)                        644.97                  646.93                  630.52                  648.75
Customer Distribution (TPC-H Q13)                                   2322.94                 2091.28                 2047.94                 2078.90
Forecasting Revenue Change (TPC-H Q14)                               789.30                  784.64                  774.75                  788.85
Top Supplier Query (TPC-H Q15)                                       514.38                  504.82                  501.20                  512.41
Parts/Supplier Relationship (TPC-H Q16)                              554.51                  552.83                  550.27                  555.50
Small-Quantity-Order Revenue (TPC-H Q17)                            1989.62                 1891.86                 1851.63                 1949.47
Large Volume Customer (TPC-H Q18)                                   5409.16                 5390.05                 5373.85                 5313.11
Discounted Revenue (TPC-H Q19)                                       118.45                  114.59                  112.49                  114.48
Potential Part Promotion (TPC-H Q20)                                 271.65                  242.58                  236.81                  256.10
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                  750.07                  751.79                  754.48                  774.02
Global Sales Opportunity Query (TPC-H Q22)                           213.65                  211.50                  218.33                  220.68

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-0-1-1           0.0           93.0         3.0      168.0     267.0
PostgreSQL-BHT-1-0-2-1           0.0           93.0         3.0      168.0     267.0
PostgreSQL-BHT-1-1-1-1           0.0           95.0         1.0      166.0     263.0
PostgreSQL-BHT-1-1-2-1           0.0           95.0         1.0      166.0     263.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-1-0-1-1           0.63
PostgreSQL-BHT-1-0-2-1           0.61
PostgreSQL-BHT-1-1-1-1           0.61
PostgreSQL-BHT-1-1-2-1           0.62

### Power@Size ((3600*SF)/(geo times))
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-1-0-1-1            5718.83
PostgreSQL-BHT-1-0-2-1            5932.44
PostgreSQL-BHT-1-1-1-1            5866.83
PostgreSQL-BHT-1-1-2-1            5816.58

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                    time [s]  count   SF  Throughput@Size
DBMS                 SF  num_experiment num_client                                       
PostgreSQL-BHT-1-0-1 1.0 1              1                 23      1  1.0          3443.48
PostgreSQL-BHT-1-0-2 1.0 1              2                 23      1  1.0          3443.48
PostgreSQL-BHT-1-1-1 1.0 1              1                 22      1  1.0          3600.00
PostgreSQL-BHT-1-1-2 1.0 1              2                 23      1  1.0          3443.48

### Workflow
                                   orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-1-0-1-1  PostgreSQL-BHT-1-0-1  1.0     1               1           1       1771156719     1771156742
PostgreSQL-BHT-1-0-2-1  PostgreSQL-BHT-1-0-2  1.0     1               1           2       1771156842     1771156865
PostgreSQL-BHT-1-1-1-1  PostgreSQL-BHT-1-1-1  1.0     1               1           1       1771156719     1771156741
PostgreSQL-BHT-1-1-2-1  PostgreSQL-BHT-1-1-2  1.0     1               1           2       1771156842     1771156865

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
﻿## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 1429s 
    Code: 1771156960
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
PostgreSQL-1-1-1024-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97594
    volume_size:20G
    volume_used:632M
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1771156960
                TENANT_BY:schema
                TENANT_NUM:2
                TENANT_VOL:False
PostgreSQL-1-1-1024-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97595
    volume_size:20G
    volume_used:632M
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1771156960
                TENANT_BY:schema
                TENANT_NUM:2
                TENANT_VOL:False

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1         10    1024       1      1  300.0           0                      0.446667                   0.446667   93.779140                                                     404830.0                                             103151.0
PostgreSQL-1-1-1024-1-2               1         10    1024       1      2  300.0           0                      0.520000                   0.523333  109.875572                                                     387205.0                                             100714.0
PostgreSQL-1-1-1024-2-1               1         10    1024       2      1  300.0           0                      0.436667                   0.436667   91.679621                                                     147800.0                                              37745.0
PostgreSQL-1-1-1024-2-2               1         10    1024       2      2  300.0           0                      0.466667                   0.460000   96.578535                                                     147249.0                                              39048.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         20    2048          2  300.0           0                          0.97                       0.97         0.0                                                     404830.0                                             101932.5
PostgreSQL-1-1-1024-2               1         20    2048          2  300.0           0                          0.90                       0.90         0.0                                                     147800.0                                              38396.5

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      340.0        1.0   2.0          10.588235
PostgreSQL-1-1-1024-2      340.0        1.0   2.0          10.588235

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
﻿## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 1405s 
    Code: 1771158396
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
PostgreSQL-1-1-1024-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97595
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
                code:1771158396
                TENANT_BY:database
                TENANT_NUM:2
                TENANT_VOL:False
PostgreSQL-1-1-1024-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97595
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
                code:1771158396
                TENANT_BY:database
                TENANT_NUM:2
                TENANT_VOL:False

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1         10    1024       1      1  300.0           0                      0.496667                   0.496667  104.276818                                                     609128.0                                              64946.0
PostgreSQL-1-1-1024-1-2               1         10    1024       1      2  300.0           0                      0.513333                   0.516667  108.475878                                                     356789.0                                              67582.0
PostgreSQL-1-1-1024-2-2               1         10    1024       2      1  300.0           0                      0.453332                   0.446665   93.778855                                                      47827.0                                              22390.0
PostgreSQL-1-1-1024-2-1               1         10    1024       2      2  300.0           0                      0.483333                   0.486667  102.177282                                                      53402.0                                              22442.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         20    2048          2  300.0           0                          1.01                       1.01         0.0                                                     609128.0                                              66264.0
PostgreSQL-1-1-1024-2               1         20    2048          2  300.0           0                          0.94                       0.93         0.0                                                      53402.0                                              22416.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      316.0        1.0   2.0          11.392405
PostgreSQL-1-1-1024-2      316.0        1.0   2.0          11.392405

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
﻿## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 1382s 
    Code: 1771159807
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
PostgreSQL-1-1-1024-0-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97595
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
                code:1771159807
                TENANT_BY:container
                TENANT_NUM:2
                TENANT_VOL:False
PostgreSQL-1-1-1024-0-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97595
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
                code:1771159807
                TENANT_BY:container
                TENANT_NUM:2
                TENANT_VOL:False
PostgreSQL-1-1-1024-1-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97595
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
                code:1771159807
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
    disk:97595
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
                code:1771159807
                TENANT_BY:container
                TENANT_NUM:2
                TENANT_VOL:False
                TENANT:1

### Execution

#### Per Pod
                           experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                       
PostgreSQL-1-1-1024-0-1-1               1         10    1024       1      1  300.0           0                      0.443332                   0.436665   91.679326                                                     133068.0                                              47522.0
PostgreSQL-1-1-1024-1-1-1               1         10    1024       1      1  300.0           0                      0.486667                   0.483333  101.477449                                                      87138.0                                              39348.0
PostgreSQL-1-1-1024-0-2-1               1         10    1024       2      1  300.0           0                      0.419999                   0.423332   88.879962                                                     110307.0                                              56126.0
PostgreSQL-1-1-1024-1-2-1               1         10    1024       2      1  300.0           0                      0.483332                   0.483332  101.477124                                                     464044.0                                             191360.0

#### Aggregated Parallel
     experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
1-1               1         20    2048          2  300.0           0                          0.93                       0.92         0.0                                                     133068.0                                              43435.0
1-2               1         20    2048          2  300.0           0                          0.90                       0.91         0.0                                                     464044.0                                             123743.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024-0 - Pods [[1, 1]]
DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024-0 - Pods [[1, 1]]
DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1]]

### Loading
                         time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-0-1      210.0        1.0   1.0          17.142857
PostgreSQL-1-1-1024-0-2      210.0        1.0   1.0          17.142857
PostgreSQL-1-1-1024-1-1      275.0        1.0   1.0          13.090909
PostgreSQL-1-1-1024-1-2      275.0        1.0   1.0          13.090909

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
﻿## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 3029s 
    Code: 1771161196
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
    disk:97595
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
                code:1771161196
                TENANT_BY:database
                TENANT_NUM:2
                TENANT_VOL:False
MySQL-1-1-1024-2 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97595
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
                code:1771161196
                TENANT_BY:database
                TENANT_NUM:2
                TENANT_VOL:False

### Execution

#### Per Pod
                    experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                
MySQL-1-1-1024-1-1               1         10    1024       1      1  300.0           0                      0.490000                   0.483333  101.477388                                                     616628.0                                             558817.0
MySQL-1-1-1024-1-2               1         10    1024       1      2  300.0           0                      0.483333                   0.486667  102.177282                                                     105991.0                                             103522.0
MySQL-1-1-1024-2-1               1         10    1024       2      1  300.0           0                      0.476665                   0.479998  100.777284                                                     172171.0                                              52948.0
MySQL-1-1-1024-2-2               1         10    1024       2      2  300.0           0                      0.520000                   0.516667  108.475886                                                     125203.0                                              47482.0

#### Aggregated Parallel
                  experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1               1         20    2048          2  300.0           0                          0.97                       0.97         0.0                                                     616628.0                                             331169.5
MySQL-1-1-1024-2               1         20    2048          2  300.0           0                          1.00                       1.00         0.0                                                     172171.0                                              50215.0

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[2, 2]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[2, 2]]

### Loading
                  time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1     1305.0        1.0   2.0           2.758621
MySQL-1-1-1024-2     1305.0        1.0   2.0           2.758621

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
﻿## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 3858s 
    Code: 1771164231
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
    disk:97595
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
                code:1771164231
                TENANT_BY:container
                TENANT_NUM:2
                TENANT_VOL:False
MySQL-1-1-1024-0-2 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97595
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
                code:1771164231
                TENANT_BY:container
                TENANT_NUM:2
                TENANT_VOL:False
MySQL-1-1-1024-1-1 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97595
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
                code:1771164231
                TENANT_BY:container
                TENANT_NUM:2
                TENANT:1
                TENANT_VOL:False
MySQL-1-1-1024-1-2 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97595
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
                code:1771164231
                TENANT_BY:container
                TENANT_NUM:2
                TENANT:1
                TENANT_VOL:False

### Execution

#### Per Pod
                      experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                  
MySQL-1-1-1024-0-1-1               1         10    1024       1      1  300.0           0                      0.480000                   0.480000  100.777595                                                     151957.0                                             102338.0
MySQL-1-1-1024-1-1-1               1         10    1024       1      1  300.0           0                      0.346667                   0.350000   73.483661                                                   78167439.0                                            7722663.0
MySQL-1-1-1024-0-2-1               1         10    1024       2      1  300.0           0                      0.453333                   0.450000   94.478979                                                     148986.0                                              30868.0
MySQL-1-1-1024-1-2-1               1         10    1024       2      1  300.0           0                      0.450000                   0.446667   93.779140                                                      56007.0                                              28646.0

#### Aggregated Parallel
     experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
1-1               1         20    2048          2  300.0           0                          0.83                       0.83         0.0                                                   78167439.0                                            3912500.5
1-2               1         20    2048          2  300.0           0                          0.90                       0.90         0.0                                                     148986.0                                              29757.0

### Workflow

#### Actual
DBMS MySQL-1-1-1024-0 - Pods [[1, 1]]
DBMS MySQL-1-1-1024-1 - Pods [[1, 1]]

#### Planned
DBMS MySQL-1-1-1024-0 - Pods [[1, 1]]
DBMS MySQL-1-1-1024-1 - Pods [[1, 1]]

### Loading
                    time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-0-1     1846.0        1.0   1.0           1.950163
MySQL-1-1-1024-0-2     1846.0        1.0   1.0           1.950163
MySQL-1-1-1024-1-1     1839.0        1.0   1.0           1.957586
MySQL-1-1-1024-1-2     1839.0        1.0   1.0           1.957586

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```







