## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 480s 
    Code: 1772631969
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['DatabaseService'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
DBS-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147561
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772631969

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 DBS-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                            62.27
Minimum Cost Supplier Query (TPC-H Q2)                        2.69
Shipping Priority (TPC-H Q3)                                  1.47
Order Priority Checking Query (TPC-H Q4)                      1.26
Local Supplier Volume (TPC-H Q5)                              1.75
Forecasting Revenue Change (TPC-H Q6)                         1.28
Forecasting Revenue Change (TPC-H Q7)                         1.66
National Market Share (TPC-H Q8)                              2.02
Product Type Profit Measure (TPC-H Q9)                        1.56
Forecasting Revenue Change (TPC-H Q10)                        1.51
Important Stock Identification (TPC-H Q11)                    1.35
Shipping Modes and Order Priority (TPC-H Q12)                 1.16
Customer Distribution (TPC-H Q13)                             1.19
Forecasting Revenue Change (TPC-H Q14)                        1.61
Top Supplier Query (TPC-H Q15)                                1.14
Parts/Supplier Relationship (TPC-H Q16)                       0.98
Small-Quantity-Order Revenue (TPC-H Q17)                      1.07
Large Volume Customer (TPC-H Q18)                             1.32
Discounted Revenue (TPC-H Q19)                                1.59
Potential Part Promotion (TPC-H Q20)                          1.35
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)           1.52
Global Sales Opportunity Query (TPC-H Q22)                    1.21

### Loading [s]
               timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
DBS-BHT-8-1-1          20.0            6.0         1.0      111.0     143.0

### Geometric Mean of Medians of Timer Run [s]
               Geo Times [s]
DBMS                        
DBS-BHT-8-1-1            0.0

### Power@Size ((3600*SF)/(geo times))
               Power@Size [~Q/h]
DBMS                            
DBS-BHT-8-1-1         6391661.94

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                           time [s]  count   SF  Throughput@Size
DBMS        SF  num_experiment num_client                                       
DBS-BHT-8-1 3.0 1              1                  3      1  3.0          79200.0

### Workflow
                 orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
DBS-BHT-8-1-1  DBS-BHT-8-1  3.0     8               1           1       1772632394     1772632397

#### Actual
DBMS DBS-BHT-8 - Pods [[1]]

#### Planned
DBMS DBS-BHT-8 - Pods [[1]]

### Ingestion - Loader
             CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DBS-BHT-8-1        2.01        0           0.0                 0.23

### Execution - Benchmarker
             CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DBS-BHT-8-1           0        0           0.0                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
