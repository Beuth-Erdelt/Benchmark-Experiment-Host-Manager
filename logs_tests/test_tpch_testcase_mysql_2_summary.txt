## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 506s 
    Code: 1748912070
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-BHT-8-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:325868736
    datadisk:8286
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912070

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MySQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                              77.77
Minimum Cost Supplier Query (TPC-H Q2)                          4.66
Shipping Priority (TPC-H Q3)                                    2.98
Order Priority Checking Query (TPC-H Q4)                        2.88
Local Supplier Volume (TPC-H Q5)                                2.64
Forecasting Revenue Change (TPC-H Q6)                           2.56
Forecasting Revenue Change (TPC-H Q7)                           3.44
National Market Share (TPC-H Q8)                                4.37
Product Type Profit Measure (TPC-H Q9)                          2.82
Forecasting Revenue Change (TPC-H Q10)                          2.66
Important Stock Identification (TPC-H Q11)                      2.85
Shipping Modes and Order Priority (TPC-H Q12)                   2.43
Customer Distribution (TPC-H Q13)                               2.19
Forecasting Revenue Change (TPC-H Q14)                          2.56
Top Supplier Query (TPC-H Q15)                                  4.68
Parts/Supplier Relationship (TPC-H Q16)                         2.91
Small-Quantity-Order Revenue (TPC-H Q17)                        1.92
Large Volume Customer (TPC-H Q18)                               2.34
Discounted Revenue (TPC-H Q19)                                  2.55
Potential Part Promotion (TPC-H Q20)                            3.07
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)             3.07
Global Sales Opportunity Query (TPC-H Q22)                      2.61

### Loading [s]
                 timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MySQL-BHT-8-1-1           1.0            4.0         3.0       12.0      27.0

### Geometric Mean of Medians of Timer Run [s]
                 Geo Times [s]
DBMS                          
MySQL-BHT-8-1-1            0.0

### Power@Size ((3600*SF)/(geo times))
                 Power@Size [~Q/h]
DBMS                              
MySQL-BHT-8-1-1         1074975.18

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                            time [s]  count  SF  Throughput@Size
DBMS          SF num_experiment num_client                                      
MySQL-BHT-8-1 1  1              1                  2      1   1          39600.0

### Workflow

#### Actual
DBMS MySQL-BHT-8 - Pods [[1]]

#### Planned
DBMS MySQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
               CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1        3.61     0.03         37.45                37.48

### Ingestion - Loader
               CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1           0        0           0.0                  0.0

### Execution - SUT
               CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1        7.33        0         37.73                37.77

### Execution - Benchmarker
               CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1           0        0           0.0                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
