## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 1136s 
    Code: 1749124058
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
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-BHT-8-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359468664
    datadisk:2756
    volume_size:30G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749124058
PostgreSQL-BHT-8-1-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359468728
    datadisk:2756
    volume_size:30G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749124058
PostgreSQL-BHT-8-1-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359468728
    datadisk:2756
    volume_size:30G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749124058
PostgreSQL-BHT-8-2-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359469096
    datadisk:2756
    volume_size:30G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749124058
PostgreSQL-BHT-8-2-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359469184
    datadisk:2756
    volume_size:30G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749124058
PostgreSQL-BHT-8-2-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359469184
    datadisk:2756
    volume_size:30G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749124058

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-1-2-1  PostgreSQL-BHT-8-1-2-2  PostgreSQL-BHT-8-2-1-1  PostgreSQL-BHT-8-2-2-1  PostgreSQL-BHT-8-2-2-2
Pricing Summary Report (TPC-H Q1)                                   2614.52                 2642.39                 2604.84                18633.87                 2624.48                 2675.74
Minimum Cost Supplier Query (TPC-H Q2)                               445.02                  441.96                  447.43                 5703.12                  433.16                  435.90
Shipping Priority (TPC-H Q3)                                         779.34                  774.85                  762.82                 7519.57                  789.58                  792.43
Order Priority Checking Query (TPC-H Q4)                            1281.22                 1286.58                 1342.62                 1306.41                 1309.83                 1313.99
Local Supplier Volume (TPC-H Q5)                                     665.83                  674.82                  686.17                  690.62                  699.38                  698.48
Forecasting Revenue Change (TPC-H Q6)                                507.17                  520.35                  520.19                  526.88                  535.80                  538.53
Forecasting Revenue Change (TPC-H Q7)                                785.13                  788.03                  798.76                 1295.23                  805.37                  797.96
National Market Share (TPC-H Q8)                                     624.63                  632.75                  647.12                  740.64                  658.46                  665.55
Product Type Profit Measure (TPC-H Q9)                              1132.25                 1164.79                 1117.45                 2016.87                 1103.52                 1110.77
Forecasting Revenue Change (TPC-H Q10)                              1265.15                 1267.20                 1286.72                 1275.40                 1300.60                 1297.94
Important Stock Identification (TPC-H Q11)                           262.01                  260.05                  265.42                  250.19                  265.08                  255.87
Shipping Modes and Order Priority (TPC-H Q12)                       1057.55                 1046.59                 1058.06                 1044.35                 1077.73                 1064.54
Customer Distribution (TPC-H Q13)                                   2065.25                 2072.03                 2072.19                 1989.10                 2001.56                 1998.74
Forecasting Revenue Change (TPC-H Q14)                               546.77                  562.86                  573.69                  560.21                  579.82                  571.89
Top Supplier Query (TPC-H Q15)                                       573.94                  582.73                  583.57                  586.54                  584.55                  586.18
Parts/Supplier Relationship (TPC-H Q16)                              586.59                  580.33                  577.89                  575.69                  576.60                  563.90
Small-Quantity-Order Revenue (TPC-H Q17)                            2033.42                 2051.03                 2053.55                 2060.93                 2111.37                 2039.19
Large Volume Customer (TPC-H Q18)                                   8056.48                 7307.63                 8689.75                 7420.83                 7240.46                 7213.62
Discounted Revenue (TPC-H Q19)                                       708.21                  717.10                  710.97                  714.35                  721.29                  718.50
Potential Part Promotion (TPC-H Q20)                                 653.03                  730.87                  638.75                  652.84                  639.70                  638.02
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                  939.45                  915.25                  907.94                 2708.81                  916.32                  913.78
Global Sales Opportunity Query (TPC-H Q22)                           266.10                  231.33                  227.50                  375.23                  216.86                  217.63

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1-1           1.0           44.0         1.0       87.0     141.0
PostgreSQL-BHT-8-1-2-1           1.0           44.0         1.0       87.0     141.0
PostgreSQL-BHT-8-1-2-2           1.0           44.0         1.0       87.0     141.0
PostgreSQL-BHT-8-2-1-1           1.0           44.0         1.0       87.0     141.0
PostgreSQL-BHT-8-2-2-1           1.0           44.0         1.0       87.0     141.0
PostgreSQL-BHT-8-2-2-2           1.0           44.0         1.0       87.0     141.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-8-1-1-1           0.92
PostgreSQL-BHT-8-1-2-1           0.91
PostgreSQL-BHT-8-1-2-2           0.92
PostgreSQL-BHT-8-2-1-1           1.40
PostgreSQL-BHT-8-2-2-1           0.91
PostgreSQL-BHT-8-2-2-2           0.91

### Power@Size ((3600*SF)/(geo times))
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-8-1-1-1            4107.36
PostgreSQL-BHT-8-1-2-1            4111.74
PostgreSQL-BHT-8-1-2-2            4092.11
PostgreSQL-BHT-8-2-1-1            2678.56
PostgreSQL-BHT-8-2-2-1            4115.93
PostgreSQL-BHT-8-2-2-2            4131.74

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                   time [s]  count  SF  Throughput@Size
DBMS                 SF num_experiment num_client                                      
PostgreSQL-BHT-8-1-1 1  1              1                 32      1   1           2475.0
PostgreSQL-BHT-8-1-2 1  1              2                 33      2   1           4800.0
PostgreSQL-BHT-8-2-1 1  2              1                 64      1   1           1237.5
PostgreSQL-BHT-8-2-2 1  2              2                 32      2   1           4950.0

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1, 2], [1, 2]]

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1      118.56     1.12          3.69                 5.36
PostgreSQL-BHT-8-1-2      118.56     1.12          3.69                 5.36

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1        2.08        0          0.02                 0.21
PostgreSQL-BHT-8-1-2        2.08        0          0.02                 0.21

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       57.45     0.98          3.69                 5.36
PostgreSQL-BHT-8-1-2      206.36     0.00          7.43                 9.05
PostgreSQL-BHT-8-2-1      402.41     0.00          6.15                 8.02
PostgreSQL-BHT-8-2-2      112.61     2.09          3.98                 5.78

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       14.05      0.0          0.27                 0.28
PostgreSQL-BHT-8-1-2        0.00      0.0          0.27                 0.28
PostgreSQL-BHT-8-2-1        0.02      0.0          0.00                 0.00
PostgreSQL-BHT-8-2-2        0.00      0.0          0.00                 0.00

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
