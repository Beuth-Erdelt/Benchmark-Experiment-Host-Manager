## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 545s 
    Code: 1773256198
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.9.3.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:18.3
    RAM:2164173209600
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1229355
    cpu_list:0-223
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    eval_parameters
        code:1773256198

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 1735.75
Minimum Cost Supplier Query (TPC-H Q2)                             495.27
Shipping Priority (TPC-H Q3)                                       578.11
Order Priority Checking Query (TPC-H Q4)                           287.24
Local Supplier Volume (TPC-H Q5)                                   565.30
Forecasting Revenue Change (TPC-H Q6)                              339.80
Forecasting Revenue Change (TPC-H Q7)                              721.02
National Market Share (TPC-H Q8)                                   382.17
Product Type Profit Measure (TPC-H Q9)                             984.52
Forecasting Revenue Change (TPC-H Q10)                            1160.79
Important Stock Identification (TPC-H Q11)                         171.32
Shipping Modes and Order Priority (TPC-H Q12)                      520.43
Customer Distribution (TPC-H Q13)                                 2001.35
Forecasting Revenue Change (TPC-H Q14)                             566.71
Top Supplier Query (TPC-H Q15)                                     428.06
Parts/Supplier Relationship (TPC-H Q16)                            419.11
Small-Quantity-Order Revenue (TPC-H Q17)                          1570.33
Large Volume Customer (TPC-H Q18)                                 6554.17
Discounted Revenue (TPC-H Q19)                                     101.73
Potential Part Promotion (TPC-H Q20)                               310.89
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                573.62
Global Sales Opportunity Query (TPC-H Q22)                         163.12

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1          18.0           18.0         2.0      207.0     247.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           0.59

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1           18849.72

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-8-1 3.0 1              1                 23      1  3.0         10330.43

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-1  3.0     8               1           1       1773256618     1773256641

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1        46.4     0.76          6.38                 9.62

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1        0.17        0           0.0                  0.0

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1         0.0     0.92          9.64                13.89

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1           0        0           0.0                  0.0

### Application Metrics

#### Loading phase: SUT deployment
                    Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
PostgreSQL-BHT-8-1                        0                                       0                                               0                          8                                      8

#### Execution phase: SUT deployment
                    Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
PostgreSQL-BHT-8-1                        0                                       0                                               0                          4                                      4

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST failed: Execution SUT contains 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
