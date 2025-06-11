## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 506s 
    Code: 1749632089
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Services
PostgreSQL-BHT-1
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1749632089 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:389393760
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749632089

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-1-1-1
Pricing Summary Report (TPC-H Q1)                                 2558.68
Minimum Cost Supplier Query (TPC-H Q2)                             440.98
Shipping Priority (TPC-H Q3)                                       772.87
Order Priority Checking Query (TPC-H Q4)                          1290.26
Local Supplier Volume (TPC-H Q5)                                   673.11
Forecasting Revenue Change (TPC-H Q6)                              508.40
Forecasting Revenue Change (TPC-H Q7)                              794.26
National Market Share (TPC-H Q8)                                   636.57
Product Type Profit Measure (TPC-H Q9)                            1154.01
Forecasting Revenue Change (TPC-H Q10)                            1275.45
Important Stock Identification (TPC-H Q11)                         254.67
Shipping Modes and Order Priority (TPC-H Q12)                     1065.38
Customer Distribution (TPC-H Q13)                                 1991.37
Forecasting Revenue Change (TPC-H Q14)                             567.41
Top Supplier Query (TPC-H Q15)                                     558.84
Parts/Supplier Relationship (TPC-H Q16)                            570.01
Small-Quantity-Order Revenue (TPC-H Q17)                          1884.79
Large Volume Customer (TPC-H Q18)                                 7194.80
Discounted Revenue (TPC-H Q19)                                     709.86
Potential Part Promotion (TPC-H Q20)                               661.73
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                920.74
Global Sales Opportunity Query (TPC-H Q22)                         248.82

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-1-1           0.0           87.0         1.0       88.0     177.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-1-1-1           0.86

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-1-1-1            4163.28

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count  SF  Throughput@Size
DBMS               SF num_experiment num_client                                      
PostgreSQL-BHT-1-1 1  1              1                 29      1   1          2731.03

### Workflow

#### Actual
DBMS PostgreSQL-BHT - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-1 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1      144.14     0.04          3.79                 5.33

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1        4.97        0           0.0                 0.73

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1      121.82        0          3.85                 5.39

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1           0        0           0.0                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST failed: Workflow not as planned
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
