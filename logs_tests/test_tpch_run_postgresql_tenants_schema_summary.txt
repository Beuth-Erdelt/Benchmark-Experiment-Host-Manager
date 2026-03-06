## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 636s 
    Code: 1772805267
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.9.1.
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
PostgreSQL-BHT-2-1-1 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147807
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772805267
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-1-2 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147807
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772805267
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-2-1 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147807
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772805267
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-2-2 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147807
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772805267
        TENANT_BY:schema
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-2-1  PostgreSQL-BHT-2-2-2
Pricing Summary Report (TPC-H Q1)                                 2079.58               2085.42               2081.47               2078.71
Minimum Cost Supplier Query (TPC-H Q2)                             468.33                471.49                444.98                459.48
Shipping Priority (TPC-H Q3)                                       711.79                706.44                661.01                664.86
Order Priority Checking Query (TPC-H Q4)                           354.66                342.12                326.43                340.80
Local Supplier Volume (TPC-H Q5)                                   631.75                620.14                600.67                638.99
Forecasting Revenue Change (TPC-H Q6)                              454.43                454.14                459.67                452.14
Forecasting Revenue Change (TPC-H Q7)                              716.52                734.54                713.47                736.23
National Market Share (TPC-H Q8)                                   416.92                429.69                356.72                384.90
Product Type Profit Measure (TPC-H Q9)                            1049.74               1014.33               1020.71                995.31
Forecasting Revenue Change (TPC-H Q10)                             583.18                562.20                581.84                565.27
Important Stock Identification (TPC-H Q11)                         162.82                167.30                163.75                180.95
Shipping Modes and Order Priority (TPC-H Q12)                      628.55                637.00                628.88                645.86
Customer Distribution (TPC-H Q13)                                 1914.55               2057.72               2020.75               2126.03
Forecasting Revenue Change (TPC-H Q14)                             767.66                774.33                747.84                785.27
Top Supplier Query (TPC-H Q15)                                     503.74                504.16                496.65                518.29
Parts/Supplier Relationship (TPC-H Q16)                            548.99                532.01                556.74                534.12
Small-Quantity-Order Revenue (TPC-H Q17)                          1663.16               1721.91               1660.84               1889.35
Large Volume Customer (TPC-H Q18)                                 5861.63               6257.22               6486.92               5711.48
Discounted Revenue (TPC-H Q19)                                     123.14                111.44                107.88                114.10
Potential Part Promotion (TPC-H Q20)                               258.77                279.05                246.15                285.84
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                742.09                742.59                746.69                743.94
Global Sales Opportunity Query (TPC-H Q22)                         215.80                210.63                210.94                214.86

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-2-1-1           0.0          119.0         3.0      203.0     328.0
PostgreSQL-BHT-2-1-2           0.0          119.0         3.0      203.0     328.0
PostgreSQL-BHT-2-2-1           0.0          119.0         3.0      203.0     328.0
PostgreSQL-BHT-2-2-2           0.0          119.0         3.0      203.0     328.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-2-1-1           0.62
PostgreSQL-BHT-2-1-2           0.62
PostgreSQL-BHT-2-2-1           0.61
PostgreSQL-BHT-2-2-2           0.62

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-2-1-1            5810.05
PostgreSQL-BHT-2-1-2            5790.64
PostgreSQL-BHT-2-2-1            5944.09
PostgreSQL-BHT-2-2-2            5776.93

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-2-1 1.0 1              1                 23      2  1.0          6886.96
PostgreSQL-BHT-2-2 1.0 1              2                 25      2  1.0          6336.00

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1  1.0     2               1           1       1772805705     1772805727
PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-1  1.0     2               1           1       1772805705     1772805728
PostgreSQL-BHT-2-2-1  PostgreSQL-BHT-2-2  1.0     2               1           2       1772805816     1772805840
PostgreSQL-BHT-2-2-2  PostgreSQL-BHT-2-2  1.0     2               1           2       1772805815     1772805839

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
