## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 513s 
    Code: 1749123427
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:362467200
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749123427

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 2593.30
Minimum Cost Supplier Query (TPC-H Q2)                             436.83
Shipping Priority (TPC-H Q3)                                       736.10
Order Priority Checking Query (TPC-H Q4)                          1272.38
Local Supplier Volume (TPC-H Q5)                                   659.77
Forecasting Revenue Change (TPC-H Q6)                              496.73
Forecasting Revenue Change (TPC-H Q7)                              775.38
National Market Share (TPC-H Q8)                                   617.19
Product Type Profit Measure (TPC-H Q9)                            1088.37
Forecasting Revenue Change (TPC-H Q10)                            1254.81
Important Stock Identification (TPC-H Q11)                         249.06
Shipping Modes and Order Priority (TPC-H Q12)                     1041.05
Customer Distribution (TPC-H Q13)                                 2081.47
Forecasting Revenue Change (TPC-H Q14)                             541.66
Top Supplier Query (TPC-H Q15)                                     556.87
Parts/Supplier Relationship (TPC-H Q16)                            554.41
Small-Quantity-Order Revenue (TPC-H Q17)                          2036.83
Large Volume Customer (TPC-H Q18)                                 7942.95
Discounted Revenue (TPC-H Q19)                                     686.88
Potential Part Promotion (TPC-H Q20)                               671.08
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                906.43
Global Sales Opportunity Query (TPC-H Q22)                         244.90

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0           29.0         1.0       90.0     129.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           0.89

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4198.36

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count  SF  Throughput@Size
DBMS               SF num_experiment num_client                                      
PostgreSQL-BHT-8-1 1  1              1                 31      1   1          2554.84

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      122.17     0.96          3.72                 4.91

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1        5.55        0          0.02                 0.49

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       89.74        0          3.82                 5.01

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       11.91        0          0.24                 0.25

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
