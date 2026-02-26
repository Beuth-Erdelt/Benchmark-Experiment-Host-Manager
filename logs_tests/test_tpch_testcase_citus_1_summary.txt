## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 864s 
    Code: 1771345642
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['Citus'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Citus-BHT-8-1-1 uses docker image citusdata/citus:13.2.0-alpine
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:98943
    cpu_list:0-63
    args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:406553
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 1
        RAM:1077382688768
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1360233
        cpu_list:0-255
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 2
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:891172
        cpu_list:0-223
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 3
        RAM:1081742745600
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:556386
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    eval_parameters
        code:1771345642
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:False

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 Citus-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                             138.49
Minimum Cost Supplier Query (TPC-H Q2)                         16.56
Shipping Priority (TPC-H Q3)                                   34.43
Order Priority Checking Query (TPC-H Q4)                       12.53
Local Supplier Volume (TPC-H Q5)                               61.52
Forecasting Revenue Change (TPC-H Q6)                          12.22
Forecasting Revenue Change (TPC-H Q7)                          44.55
National Market Share (TPC-H Q8)                               55.27
Product Type Profit Measure (TPC-H Q9)                         46.31
Forecasting Revenue Change (TPC-H Q10)                         25.17
Important Stock Identification (TPC-H Q11)                      4.57
Shipping Modes and Order Priority (TPC-H Q12)                  16.31
Customer Distribution (TPC-H Q13)                              17.05
Forecasting Revenue Change (TPC-H Q14)                         13.15
Top Supplier Query (TPC-H Q15)                                 14.85
Parts/Supplier Relationship (TPC-H Q16)                         3.24
Small-Quantity-Order Revenue (TPC-H Q17)                       28.50
Large Volume Customer (TPC-H Q18)                              24.69
Discounted Revenue (TPC-H Q19)                                 23.02
Potential Part Promotion (TPC-H Q20)                           19.81
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)            36.37
Global Sales Opportunity Query (TPC-H Q22)                     14.66

### Loading [s]
                 timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
Citus-BHT-8-1-1          18.0            3.0         1.0       80.0     107.0

### Geometric Mean of Medians of Timer Run [s]
                 Geo Times [s]
DBMS                          
Citus-BHT-8-1-1           0.02

### Power@Size ((3600*SF)/(geo times))
                 Power@Size [~Q/h]
DBMS                              
Citus-BHT-8-1-1          164766.43

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                             time [s]  count   SF  Throughput@Size
DBMS          SF  num_experiment num_client                                       
Citus-BHT-8-1 1.0 1              1                  2      1  1.0          39600.0

### Workflow
                     orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
Citus-BHT-8-1-1  Citus-BHT-8-1  1.0     8               1           1       1771346436     1771346438

#### Actual
DBMS Citus-BHT-8 - Pods [[1]]

#### Planned
DBMS Citus-BHT-8 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
