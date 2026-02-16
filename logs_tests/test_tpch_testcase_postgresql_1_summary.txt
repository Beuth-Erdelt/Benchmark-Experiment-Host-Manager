## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 775s 
    Code: 1759316196
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.12.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker34.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:17.5
    RAM:1081649909760
    CPU:AMD EPYC 7453 28-Core Processor
    Cores:56
    host:6.8.0-60-generic
    node:cl-worker34
    disk:320526368
    datadisk:2757
    cpu_list:0-55
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1759316196

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 1036.65
Minimum Cost Supplier Query (TPC-H Q2)                             198.63
Shipping Priority (TPC-H Q3)                                       440.72
Order Priority Checking Query (TPC-H Q4)                           227.97
Local Supplier Volume (TPC-H Q5)                                   403.75
Forecasting Revenue Change (TPC-H Q6)                              217.37
Forecasting Revenue Change (TPC-H Q7)                              437.93
National Market Share (TPC-H Q8)                                   246.66
Product Type Profit Measure (TPC-H Q9)                             727.34
Forecasting Revenue Change (TPC-H Q10)                             416.14
Important Stock Identification (TPC-H Q11)                          81.36
Shipping Modes and Order Priority (TPC-H Q12)                      305.44
Customer Distribution (TPC-H Q13)                                  909.72
Forecasting Revenue Change (TPC-H Q14)                             240.98
Top Supplier Query (TPC-H Q15)                                     248.57
Parts/Supplier Relationship (TPC-H Q16)                            285.11
Small-Quantity-Order Revenue (TPC-H Q17)                           890.08
Large Volume Customer (TPC-H Q18)                                 2802.11
Discounted Revenue (TPC-H Q19)                                      62.23
Potential Part Promotion (TPC-H Q20)                               147.88
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                374.33
Global Sales Opportunity Query (TPC-H Q22)                         121.12

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1          19.0           10.0         5.0      301.0     339.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           0.35

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1           10943.16

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-8-1 1.0 1              1                 16      1  1.0           4950.0

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-1  1.0     8               1           1       1759316682     1759316698

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
