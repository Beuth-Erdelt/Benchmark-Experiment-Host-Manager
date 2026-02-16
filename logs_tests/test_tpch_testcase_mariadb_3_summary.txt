## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 6081s 
    Code: 1748919033
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MariaDB'].
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
MariaDB-BHT-8-1-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515964
    datadisk:2090
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033
MariaDB-BHT-8-1-2-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515968
    datadisk:2090
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033
MariaDB-BHT-8-1-2-2 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515968
    datadisk:2090
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033
MariaDB-BHT-8-2-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515956
    datadisk:2095
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033
MariaDB-BHT-8-2-2-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515960
    datadisk:2095
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033
MariaDB-BHT-8-2-2-2 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515960
    datadisk:2095
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MariaDB-BHT-8-1-1-1  MariaDB-BHT-8-1-2-1  MariaDB-BHT-8-1-2-2  MariaDB-BHT-8-2-1-1  MariaDB-BHT-8-2-2-1  MariaDB-BHT-8-2-2-2
Pricing Summary Report (TPC-H Q1)                               25974.35             24684.85             24739.11             25744.04             25961.78             25820.11
Minimum Cost Supplier Query (TPC-H Q2)                           1453.22              1677.86              1703.46              1762.40              1618.89              1619.03
Shipping Priority (TPC-H Q3)                                     5221.88              6529.53              6493.69              7216.41              6423.40              6417.20
Order Priority Checking Query (TPC-H Q4)                         1075.72              1336.18              1341.60              1323.22              1288.26              1287.75
Local Supplier Volume (TPC-H Q5)                                 3287.17              3783.79              3852.58              3482.38              3748.09              3748.27
Forecasting Revenue Change (TPC-H Q6)                            2801.76              3999.80              3944.80              3313.50              2961.49              2943.89
Forecasting Revenue Change (TPC-H Q7)                            3639.82              3945.00              4008.61              3805.95              4300.03              4300.00
National Market Share (TPC-H Q8)                                 6468.87              7603.58              7262.87              6879.16              7697.18              7697.15
Product Type Profit Measure (TPC-H Q9)                           5802.95              6661.06              6938.45              6114.94              6373.02              6372.93
Forecasting Revenue Change (TPC-H Q10)                           2955.81              2928.45              2966.85              2984.05              3205.20              3202.19
Important Stock Identification (TPC-H Q11)                        382.23               442.78               435.66               413.34               494.31               498.47
Shipping Modes and Order Priority (TPC-H Q12)                   11413.65             12428.21             12536.94             11768.67             12604.75             12604.79
Customer Distribution (TPC-H Q13)                                9852.55             11791.98             12055.63              9988.15             11283.96             11281.52
Forecasting Revenue Change (TPC-H Q14)                          31100.58             36921.43             40084.43             30354.96             35245.42             35245.52
Top Supplier Query (TPC-H Q15)                                   6228.19              6508.01              6396.66              6582.36              6575.85              6504.29
Parts/Supplier Relationship (TPC-H Q16)                           629.99               643.59               623.90               671.43               665.07               664.95
Small-Quantity-Order Revenue (TPC-H Q17)                          160.92               150.71               153.73               146.73               151.15               150.50
Large Volume Customer (TPC-H Q18)                               10162.65             11347.40             11718.83             10464.66             11239.03             11334.00
Discounted Revenue (TPC-H Q19)                                    264.98               285.77               294.18               287.03               272.64               275.01
Potential Part Promotion (TPC-H Q20)                              527.27               577.32               685.68               586.09               634.04               635.37
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)            194454.66            222543.33            222766.92            197089.34            213727.42            213737.84
Global Sales Opportunity Query (TPC-H Q22)                        402.35               395.79               372.82               397.17               442.14               441.05

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1-1           1.0          696.0         5.0     3089.0    3797.0
MariaDB-BHT-8-1-2-1           1.0          696.0         5.0     3089.0    3797.0
MariaDB-BHT-8-1-2-2           1.0          696.0         5.0     3089.0    3797.0
MariaDB-BHT-8-2-1-1           1.0          696.0         5.0     3089.0    3797.0
MariaDB-BHT-8-2-2-1           1.0          696.0         5.0     3089.0    3797.0
MariaDB-BHT-8-2-2-2           1.0          696.0         5.0     3089.0    3797.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MariaDB-BHT-8-1-1-1           3.22
MariaDB-BHT-8-1-2-1           3.59
MariaDB-BHT-8-1-2-2           3.64
MariaDB-BHT-8-2-1-1           3.44
MariaDB-BHT-8-2-2-1           3.58
MariaDB-BHT-8-2-2-2           3.60

### Power@Size ((3600*SF)/(geo times))
                     Power@Size [~Q/h]
DBMS                                  
MariaDB-BHT-8-1-1-1            1154.15
MariaDB-BHT-8-1-2-1            1035.86
MariaDB-BHT-8-1-2-2            1022.45
MariaDB-BHT-8-2-1-1            1080.60
MariaDB-BHT-8-2-2-1            1036.64
MariaDB-BHT-8-2-2-2            1036.84

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                time [s]  count  SF  Throughput@Size
DBMS              SF num_experiment num_client                                      
MariaDB-BHT-8-1-1 1  1              1                328      1   1           241.46
MariaDB-BHT-8-1-2 1  1              2                376      2   1           421.28
MariaDB-BHT-8-2-1 1  2              1                338      1   1           234.32
MariaDB-BHT-8-2-2 1  2              2                363      2   1           436.36

### Workflow

#### Actual
DBMS MariaDB-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned
DBMS MariaDB-BHT-8 - Pods [[1, 2], [1, 2]]

### Ingestion - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1     2263.77     2.11          9.81                 9.84
MariaDB-BHT-8-1-2     2263.77     2.11          9.81                 9.84

### Ingestion - Loader
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1        7.69     0.01           0.5                 1.16
MariaDB-BHT-8-1-2        7.69     0.01           0.5                 1.16

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1      318.25      1.0          9.88                 9.91
MariaDB-BHT-8-1-2      678.67      2.0          9.89                 9.92
MariaDB-BHT-8-2-1     3375.23      1.0         12.41                12.63
MariaDB-BHT-8-2-2      650.38      2.0          2.56                 2.81

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1       14.94     0.00          0.26                 0.26
MariaDB-BHT-8-1-2       25.00     0.01          0.72                 0.74
MariaDB-BHT-8-2-1       14.09     0.01          0.25                 0.27
MariaDB-BHT-8-2-2       31.69     0.06          0.75                 0.78

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
