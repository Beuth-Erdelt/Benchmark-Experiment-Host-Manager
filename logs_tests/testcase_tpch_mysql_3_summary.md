## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 1241s 
    Code: 1748912641
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
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MySQL-BHT-8-1-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384432
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-1-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384432
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-1-2-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384432
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-2-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384416
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-2-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384420
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-2-2-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384420
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MySQL-BHT-8-1-1-1  MySQL-BHT-8-1-2-1  MySQL-BHT-8-1-2-2  MySQL-BHT-8-2-1-1  MySQL-BHT-8-2-2-1  MySQL-BHT-8-2-2-2
Pricing Summary Report (TPC-H Q1)                                77.71              71.17             113.27              90.10              68.93              81.12
Minimum Cost Supplier Query (TPC-H Q2)                            4.07               3.44               3.64              16.93               4.26               3.92
Shipping Priority (TPC-H Q3)                                      2.18               1.87               2.57               3.00               1.75               2.78
Order Priority Checking Query (TPC-H Q4)                          1.64               1.53               3.12               3.66               1.49               2.79
Local Supplier Volume (TPC-H Q5)                                  1.87               1.74               3.57               2.56               1.77               3.41
Forecasting Revenue Change (TPC-H Q6)                             1.33               1.32               2.57               2.35               1.45               2.29
Forecasting Revenue Change (TPC-H Q7)                             1.90               2.24               3.55               2.75               1.87               2.75
National Market Share (TPC-H Q8)                                  3.18               1.92               3.07               3.26               2.51               2.98
Product Type Profit Measure (TPC-H Q9)                            1.94               1.69               2.81               2.76               1.92               2.73
Forecasting Revenue Change (TPC-H Q10)                            2.34               1.73               2.02               3.02               1.69               2.82
Important Stock Identification (TPC-H Q11)                        2.17               1.62               2.62               2.36               1.46               2.78
Shipping Modes and Order Priority (TPC-H Q12)                     2.92               1.41               3.14               2.75               1.71               2.73
Customer Distribution (TPC-H Q13)                                 2.79               1.47               2.62               2.19               1.32               2.65
Forecasting Revenue Change (TPC-H Q14)                            1.91               1.28               2.55               2.31               1.13               2.48
Top Supplier Query (TPC-H Q15)                                    4.25               2.78               4.84               5.21               3.27               4.68
Parts/Supplier Relationship (TPC-H Q16)                           2.79               1.84               3.10               2.31               2.02               3.30
Small-Quantity-Order Revenue (TPC-H Q17)                          2.13               1.24               5.14               2.00               1.73               2.81
Large Volume Customer (TPC-H Q18)                                 2.22               1.51               2.48               2.56               2.05               3.17
Discounted Revenue (TPC-H Q19)                                    2.26               1.71               2.63               2.48               2.09               2.37
Potential Part Promotion (TPC-H Q20)                              2.61               1.49               3.36               2.88               1.79               3.23
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)               3.06               1.52               3.19               3.00               1.87               3.14
Global Sales Opportunity Query (TPC-H Q22)                        2.52               1.74               2.90               2.54               2.01               2.95

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MySQL-BHT-8-1-1-1           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-1-2-1           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-1-2-2           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-2-1-1           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-2-2-1           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-2-2-2           1.0            4.0         9.0       20.0      41.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MySQL-BHT-8-1-1-1            0.0
MySQL-BHT-8-1-2-1            0.0
MySQL-BHT-8-1-2-2            0.0
MySQL-BHT-8-2-1-1            0.0
MySQL-BHT-8-2-2-1            0.0
MySQL-BHT-8-2-2-2            0.0

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MySQL-BHT-8-1-1-1         1287048.59
MySQL-BHT-8-1-2-1         1775137.53
MySQL-BHT-8-1-2-2         1003150.78
MySQL-BHT-8-2-1-1         1034211.47
MySQL-BHT-8-2-2-1         1630827.76
MySQL-BHT-8-2-2-2         1050194.94

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                              time [s]  count  SF  Throughput@Size
DBMS            SF num_experiment num_client                                      
MySQL-BHT-8-1-1 1  1              1                  2      1   1          39600.0
MySQL-BHT-8-1-2 1  1              2                  3      2   1          52800.0
MySQL-BHT-8-2-1 1  2              1                  2      1   1          39600.0
MySQL-BHT-8-2-2 1  2              2                  3      2   1          52800.0

### Workflow

#### Actual
DBMS MySQL-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned
DBMS MySQL-BHT-8 - Pods [[1, 2], [1, 2]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        4.72     0.02         37.47                45.51
MySQL-BHT-8-1-2        4.72     0.02         37.47                45.51

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1           0        0           0.0                  0.0
MySQL-BHT-8-1-2           0        0           0.0                  0.0

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        0.00     0.00         37.47                45.51
MySQL-BHT-8-1-2        1.35     0.00         37.75                45.78
MySQL-BHT-8-2-1      255.00     0.00         75.20                91.06
MySQL-BHT-8-2-2        0.00     0.02         37.46                45.29

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        0.00      0.0           0.0                  0.0
MySQL-BHT-8-1-2        0.00      0.0           0.0                  0.0
MySQL-BHT-8-2-1        0.00      0.0           0.0                  0.0
MySQL-BHT-8-2-2        0.03      0.0           0.0                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]
TEST failed: Execution SUT contains 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
