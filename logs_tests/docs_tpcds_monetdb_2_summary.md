## Show Summary

### Workload
TPC-DS Queries SF=30
    Type: tpcds
    Duration: 2276s 
    Code: 1772479408
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=30) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 14400.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Database is persisted to disk of type shared and size 1000Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MonetDB-BHT-8-1-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191991
    volume_size:1000G
    volume_used:75G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772479408
MonetDB-BHT-8-1-2-1 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191993
    volume_size:1000G
    volume_used:75G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772479408
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191985
    volume_size:1000G
    volume_used:74G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772479408
MonetDB-BHT-8-2-2-1 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191988
    volume_size:1000G
    volume_used:74G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772479408

### Errors (failed queries)
            MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1
TPC-DS Q90                 True                 True                 True                 True
TPC-DS Q90
MonetDB-BHT-8-1-2-1: numRun 1: : java.sql.SQLException: division by zero.
MonetDB-BHT-8-2-2-1: numRun 1: : java.sql.SQLException: division by zero.
MonetDB-BHT-8-1-1-1: numRun 1: : java.sql.SQLException: division by zero.
MonetDB-BHT-8-2-1-1: numRun 1: : java.sql.SQLException: division by zero.

### Warnings (result mismatch)
               MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1
TPC-DS Q39a+b                 True                False                 True                 True

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1
TPC-DS Q1                  2826.56                62.55              2512.90                65.91
TPC-DS Q2                  8435.85               217.23              7983.39               205.07
TPC-DS Q3                 19638.00               308.97             17956.18               318.85
TPC-DS Q4                 48656.34              4318.13             47250.61              4069.01
TPC-DS Q5                 61212.16              1307.72             62282.62              1303.80
TPC-DS Q6                  1191.94               545.45              1251.95               356.28
TPC-DS Q7                 34696.43               129.74             33854.55               152.15
TPC-DS Q8                   419.65                13.26               199.14                11.30
TPC-DS Q9                  1017.37               733.66               949.91               645.32
TPC-DS Q10               115826.34                50.80            115181.32                52.48
TPC-DS Q11                 2369.69              1800.28              2334.08              1581.88
TPC-DS Q12                  284.16               129.29               353.36               131.39
TPC-DS Q13                  393.37               255.94               381.72               265.08
TPC-DS Q14a+b                61.98                38.42                53.15                26.46
TPC-DS Q15                  126.07               138.27               115.81               133.59
TPC-DS Q16                50886.81             39387.54             50040.85             39240.87
TPC-DS Q17                12354.78              2230.10             12322.87              2291.14
TPC-DS Q18                 3756.94               512.79              4039.04               566.11
TPC-DS Q19                  359.42               175.92               277.55               173.71
TPC-DS Q20                  122.11                98.86               135.08               128.17
TPC-DS Q21                 7585.90               108.21              7721.92               119.27
TPC-DS Q22                 2596.31               244.49              2431.62               344.44
TPC-DS Q23a+b               935.17               629.97              1031.56               644.73
TPC-DS Q24a+b              3390.77              3167.91              3801.41              3172.05
TPC-DS Q25                  838.72               660.20               746.02               669.47
TPC-DS Q26                  140.51               136.72               146.48               165.09
TPC-DS Q27                 6635.07               867.54              7005.99               861.01
TPC-DS Q28                 1834.76              1026.56              1796.13              1069.73
TPC-DS Q29                  731.26               683.28               816.55               675.38
TPC-DS Q30                  219.34                18.40               174.29                32.38
TPC-DS Q31                 2665.72              1214.38              2557.54              1163.32
TPC-DS Q32                  153.25               137.98               138.89               130.84
TPC-DS Q33                  329.03                78.56               144.57                80.47
TPC-DS Q34                 2003.90               335.00              1667.71               337.43
TPC-DS Q35                   33.18                28.02                35.80                27.13
TPC-DS Q36                  784.55               753.23               730.25               729.42
TPC-DS Q37                  461.13               511.49               435.50               344.97
TPC-DS Q38                    5.61                 6.06                 5.37                 5.29
TPC-DS Q39a+b                12.90                10.01                 9.03                 8.97
TPC-DS Q40                 1696.95               498.46              2194.12               547.27
TPC-DS Q41                    6.09                 5.64                 6.07                 5.23
TPC-DS Q42                   91.93                69.45                92.81                74.36
TPC-DS Q43                  266.83               231.77               302.81               257.88
TPC-DS Q44                  245.38               246.25               270.45               227.70
TPC-DS Q45                  193.67               136.94               170.82               144.34
TPC-DS Q46                  302.86               193.60               269.31               192.79
TPC-DS Q47                  232.44               142.66               242.17               139.36
TPC-DS Q48                  164.19               167.37               168.61               167.43
TPC-DS Q49                 7430.78               949.56              7459.57              1012.68
TPC-DS Q50                  781.49               619.02               865.88               629.30
TPC-DS Q51                   94.30               116.72               103.25                90.37
TPC-DS Q52                   64.41                61.23                64.51                63.13
TPC-DS Q53                  123.76                85.27                98.40                89.21
TPC-DS Q54                 2030.80               151.17              2157.87               148.46
TPC-DS Q55                   71.84                64.50                70.98                50.32
TPC-DS Q56                 1598.46              1633.47              1668.59              1641.33
TPC-DS Q57                  218.59               117.96               209.82               116.57
TPC-DS Q58                 1374.24               427.65              1533.40               454.38
TPC-DS Q59                  914.30               812.16               927.35               822.67
TPC-DS Q60                 3039.10              3060.70              3033.69              3070.00
TPC-DS Q61                  241.43               177.60               235.55               190.22
TPC-DS Q62                  378.38               252.87               339.74               254.04
TPC-DS Q63                  151.45               102.17               118.79               108.03
TPC-DS Q64                10251.22              2252.86             10200.66              2163.83
TPC-DS Q65                  194.27               205.60               184.99               209.12
TPC-DS Q66                 1642.17              1417.15              1769.73              1415.39
TPC-DS Q67                   16.96                17.03                16.83                16.22
TPC-DS Q68                  256.01               325.09               263.94               277.61
TPC-DS Q69                   35.85                34.39                37.04                35.10
TPC-DS Q70                  381.16                11.87               435.16                11.61
TPC-DS Q71                  176.05               126.83               189.09               128.07
TPC-DS Q72                 1587.83               629.29              1446.11               646.11
TPC-DS Q73                   94.93                86.82                79.04                79.75
TPC-DS Q74                  552.13               499.24               535.68               458.69
TPC-DS Q75                 5659.66              3224.52              5847.85              3236.84
TPC-DS Q76                21541.68              6118.99             21848.77              5005.27
TPC-DS Q77                  724.31               502.99               851.97               571.36
TPC-DS Q78                 6986.43              2815.09              7061.53              3056.98
TPC-DS Q79                  177.69               150.95               149.61               150.41
TPC-DS Q80                 6015.40              5942.31              6175.09              5950.51
TPC-DS Q81                  211.11                24.02               123.87                22.17
TPC-DS Q82                  484.13               401.15               467.56               501.44
TPC-DS Q83                   20.68                23.56                21.20                20.59
TPC-DS Q84                  114.92                37.32                62.61                24.08
TPC-DS Q85                  424.98               375.37               430.98               397.02
TPC-DS Q86                  166.25               250.17               157.58               239.26
TPC-DS Q87                   16.24                 8.34                 7.67                 6.71
TPC-DS Q88                  731.94               657.34               707.60               665.00
TPC-DS Q89                  179.08               188.31               173.58               153.14
TPC-DS Q91                  247.89                29.74               201.08                26.64
TPC-DS Q92                  123.74               136.88               135.54               136.20
TPC-DS Q93                 1919.05              1879.40              1910.63              1891.93
TPC-DS Q94                35739.82             35444.00             35666.21             32985.20
TPC-DS Q95                36990.16             34054.68             33622.06             36310.39
TPC-DS Q96                   35.80                36.00                36.09                34.71
TPC-DS Q97                   62.38                50.63                65.17                44.29
TPC-DS Q98                  131.69               128.08               125.96               101.95
TPC-DS Q99                  267.73               267.17               280.21               268.54

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0          257.0        11.0     1070.0    1376.0
MonetDB-BHT-8-1-2-1           1.0          257.0        11.0     1070.0    1376.0
MonetDB-BHT-8-2-1-1           1.0          257.0        11.0     1070.0    1376.0
MonetDB-BHT-8-2-2-1           1.0          257.0        11.0     1070.0    1376.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1           0.61
MonetDB-BHT-8-1-2-1           0.25
MonetDB-BHT-8-2-1-1           0.58
MonetDB-BHT-8-2-2-1           0.25

### Power@Size ((3600*SF)/(geo times))
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1          176269.76
MonetDB-BHT-8-1-2-1          425439.59
MonetDB-BHT-8-2-1-1          185272.31
MonetDB-BHT-8-2-2-1          433826.07

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count    SF  Throughput@Size
DBMS              SF   num_experiment num_client                                        
MonetDB-BHT-8-1-1 30.0 1              1                566      1  30.0         18699.65
MonetDB-BHT-8-1-2 30.0 1              2                177      1  30.0         59796.61
MonetDB-BHT-8-2-1 30.0 2              1                561      1  30.0         18866.31
MonetDB-BHT-8-2-2 30.0 2              2                178      1  30.0         59460.67

### Workflow
                             orig_name    SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-1  30.0     8               1           1       1772479577     1772480143
MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-1-2  30.0     8               1           2       1772480273     1772480450
MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-1  30.0     8               2           1       1772480734     1772481295
MonetDB-BHT-8-2-2-1  MonetDB-BHT-8-2-2  30.0     8               2           2       1772481429     1772481607

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1     2985.66    16.74         42.76                42.83
MonetDB-BHT-8-1-2     2504.62    18.74         49.43                49.52
MonetDB-BHT-8-2-1    12931.64    15.30         46.08                46.16
MonetDB-BHT-8-2-2     2366.11    20.23         46.50                46.58

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1       13.59     0.20          0.32                 0.33
MonetDB-BHT-8-1-2       13.59     0.01          0.32                 0.33
MonetDB-BHT-8-2-1       15.11     0.02          0.30                 0.31
MonetDB-BHT-8-2-2       15.11     0.18          0.30                 0.31

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST failed: SQL errors
TEST failed: SQL warnings (result mismatch)
TEST passed: Workflow as planned
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
