## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 562s 
    Code: 1731423235
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MonetDB-BHT-8-1-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:352155712
    datadisk:3933059
    volume_size:30G
    volume_used:3.8G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:352154400
    datadisk:3933061
    volume_size:30G
    volume_used:3.8G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-2-1-1
TPC-DS Q1                   486.60               446.46
TPC-DS Q2                   735.75               496.80
TPC-DS Q3                  1769.81               659.53
TPC-DS Q4                  3358.36              2602.90
TPC-DS Q5                  3171.96              2093.09
TPC-DS Q6                   504.90               308.74
TPC-DS Q7                  1879.38              1008.73
TPC-DS Q8                   659.66               212.56
TPC-DS Q9                   286.20               205.52
TPC-DS Q10                 5364.11              4483.40
TPC-DS Q11                  697.10               673.49
TPC-DS Q12                  356.90               273.96
TPC-DS Q13                  202.20               170.23
TPC-DS Q14a+b              2933.79              2743.93
TPC-DS Q15                   31.66                27.08
TPC-DS Q16                 1167.22               745.83
TPC-DS Q17                  338.52               228.60
TPC-DS Q18                  381.40               277.50
TPC-DS Q19                  114.67                78.70
TPC-DS Q20                   30.87                30.24
TPC-DS Q21                 3169.38              1899.49
TPC-DS Q22                 2379.59              1619.44
TPC-DS Q23a+b              2909.42              2865.39
TPC-DS Q24a+b               776.45               451.26
TPC-DS Q25                  143.88               114.63
TPC-DS Q26                   62.46                45.48
TPC-DS Q27                  125.82               110.59
TPC-DS Q28                   72.60                68.92
TPC-DS Q29                  110.84               110.92
TPC-DS Q30                  172.32               121.37
TPC-DS Q31                  467.73               275.80
TPC-DS Q32                   18.83                19.72
TPC-DS Q33                  298.00               124.45
TPC-DS Q34                  742.48               335.74
TPC-DS Q35                   92.56                95.23
TPC-DS Q36                   91.34                92.79
TPC-DS Q37                   72.14                82.98
TPC-DS Q38                  197.99               209.99
TPC-DS Q39a+b              2040.00              1667.93
TPC-DS Q40                  792.22               181.19
TPC-DS Q41                   20.45                 8.41
TPC-DS Q42                   26.41                24.63
TPC-DS Q43                   61.78                74.05
TPC-DS Q44                  710.50               579.30
TPC-DS Q45                   31.67                28.30
TPC-DS Q46                  280.54                97.61
TPC-DS Q47                  268.06               259.01
TPC-DS Q48                  108.05               112.13
TPC-DS Q49                  564.18               281.98
TPC-DS Q50                  220.37               127.77
TPC-DS Q51                  632.36               592.09
TPC-DS Q52                   27.67                21.20
TPC-DS Q53                   31.81                26.92
TPC-DS Q54                   28.68                23.02
TPC-DS Q55                   16.55                17.33
TPC-DS Q56                   72.80                52.79
TPC-DS Q57                  137.53                88.66
TPC-DS Q58                   64.60                44.84
TPC-DS Q59                  126.84               100.64
TPC-DS Q60                   25.41                26.17
TPC-DS Q61                   87.56                44.10
TPC-DS Q62                  469.55               129.58
TPC-DS Q63                   26.61                37.29
TPC-DS Q64                  887.89               377.60
TPC-DS Q65                  141.28                99.52
TPC-DS Q66                  494.04               680.16
TPC-DS Q67                  701.38               660.23
TPC-DS Q68                  221.30                40.34
TPC-DS Q69                   30.22                21.72
TPC-DS Q70                  449.74               210.09
TPC-DS Q71                  123.15                68.38
TPC-DS Q72                 1045.01               395.32
TPC-DS Q73                   27.43                26.80
TPC-DS Q74                  182.78               193.39
TPC-DS Q75                  798.84               742.67
TPC-DS Q76                  520.86               470.76
TPC-DS Q77                  102.27                89.61
TPC-DS Q78                  800.57               786.99
TPC-DS Q79                   80.46               281.73
TPC-DS Q80                  427.69               464.60
TPC-DS Q81                  155.50                61.77
TPC-DS Q82                  104.57               199.35
TPC-DS Q83                  106.50                51.99
TPC-DS Q84                  333.50                50.06
TPC-DS Q85                  126.02                87.67
TPC-DS Q86                   29.07                37.32
TPC-DS Q87                  277.78               274.00
TPC-DS Q88                  440.20               142.21
TPC-DS Q89                   33.32                39.56
TPC-DS Q90                   29.34                18.02
TPC-DS Q91                  177.66                60.11
TPC-DS Q92                   13.51                14.14
TPC-DS Q93                  100.60                93.75
TPC-DS Q94                  411.45                35.92
TPC-DS Q95                  141.73               151.27
TPC-DS Q96                   13.54                16.58
TPC-DS Q97                  196.04               215.72
TPC-DS Q98                   40.15                43.13
TPC-DS Q99                   61.77               106.40

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0          125.0         7.0      100.0     243.0
MonetDB-BHT-8-2-1-1           1.0          125.0         7.0      100.0     243.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1           0.21
MonetDB-BHT-8-2-1-1           0.15

### Power@Size
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           18236.61
MonetDB-BHT-8-2-1-1           25084.76

### Throughput@Size
                                                time [s]  count  SF  Throughput@Size [~GB/h]
DBMS              SF num_experiment num_client                                              
MonetDB-BHT-8-1-1 1  1              1                 83      1   1                   954.22
MonetDB-BHT-8-2-1 1  2              1                 68      1   1                  1164.71

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1], [1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1], [1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
