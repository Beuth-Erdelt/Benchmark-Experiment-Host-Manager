## Show Summary

### Workload
TPC-H Queries SF=0.1
    Type: tpch
    Duration: 329s 
    Code: 1750049054
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=0.1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.8.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393429500
    datadisk:316
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750049054

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-1-1-1
Pricing Summary Report (TPC-H Q1)                                  459.53
Minimum Cost Supplier Query (TPC-H Q2)                              88.93
Shipping Priority (TPC-H Q3)                                       123.13
Order Priority Checking Query (TPC-H Q4)                           234.38
Local Supplier Volume (TPC-H Q5)                                   107.00
Forecasting Revenue Change (TPC-H Q6)                               88.09
Forecasting Revenue Change (TPC-H Q7)                              180.83
National Market Share (TPC-H Q8)                                   105.29
Product Type Profit Measure (TPC-H Q9)                             300.61
Forecasting Revenue Change (TPC-H Q10)                             144.60
Important Stock Identification (TPC-H Q11)                          48.95
Shipping Modes and Order Priority (TPC-H Q12)                      207.60
Customer Distribution (TPC-H Q13)                                  168.21
Forecasting Revenue Change (TPC-H Q14)                              96.50
Top Supplier Query (TPC-H Q15)                                      89.79
Parts/Supplier Relationship (TPC-H Q16)                            118.98
Small-Quantity-Order Revenue (TPC-H Q17)                           188.01
Large Volume Customer (TPC-H Q18)                                  614.75
Discounted Revenue (TPC-H Q19)                                     125.38
Potential Part Promotion (TPC-H Q20)                               100.83
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                173.64
Global Sales Opportunity Query (TPC-H Q22)                          69.02

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-1-1           0.0            7.0         2.0       18.0      29.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-1-1-1           0.14

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-1-1-1            2508.05

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-1-1 0.1 1              1                  5      1  0.1           1584.0

### Workflow

#### Actual
DBMS PostgreSQL-BHT - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-1 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST failed: Workflow not as planned
