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
