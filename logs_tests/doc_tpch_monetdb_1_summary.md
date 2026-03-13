## Show Summary

### Workload
TPC-H Queries SF=100
    Type: tpch
    Duration: 4180s 
    Code: 1772645407
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 900.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Database is persisted to disk of type shared and size 1000Gi. Persistent storage is removed at experiment start.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:723460
    volume_size:1000G
    volume_used:189G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:512Gi
    limits_memory:512Gi
    eval_parameters
        code:1772645407

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MonetDB-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                            128180.56
Minimum Cost Supplier Query (TPC-H Q2)                         1995.21
Shipping Priority (TPC-H Q3)                                   6965.39
Order Priority Checking Query (TPC-H Q4)                       8190.85
Local Supplier Volume (TPC-H Q5)                               6144.52
Forecasting Revenue Change (TPC-H Q6)                          4432.66
Forecasting Revenue Change (TPC-H Q7)                          4015.81
National Market Share (TPC-H Q8)                              14388.89
Product Type Profit Measure (TPC-H Q9)                         8715.64
Forecasting Revenue Change (TPC-H Q10)                         6958.69
Important Stock Identification (TPC-H Q11)                      807.69
Shipping Modes and Order Priority (TPC-H Q12)                  1959.25
Customer Distribution (TPC-H Q13)                             31358.06
Forecasting Revenue Change (TPC-H Q14)                         4291.66
Top Supplier Query (TPC-H Q15)                                 1669.79
Parts/Supplier Relationship (TPC-H Q16)                        3115.38
Small-Quantity-Order Revenue (TPC-H Q17)                      19847.18
Large Volume Customer (TPC-H Q18)                              6856.98
Discounted Revenue (TPC-H Q19)                                 3489.49
Potential Part Promotion (TPC-H Q20)                           2668.23
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)          229517.69
Global Sales Opportunity Query (TPC-H Q22)                     1661.89

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1          17.0          816.0        12.0     3421.0    4318.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           6.95

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           55451.39

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                 time [s]  count     SF  Throughput@Size
DBMS            SF    num_experiment num_client                                         
MonetDB-BHT-8-1 100.0 1              1                514      1  100.0         15408.56

### Workflow
                         orig_name     SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1  MonetDB-BHT-8-1  100.0     8               1           1       1772648991     1772649505

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     6849.56     10.2        184.81               184.81

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     1290.15     2.33           0.1                39.84

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1    10323.55     68.8        242.53               242.54

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       25.21     0.09          0.43                 0.44

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
