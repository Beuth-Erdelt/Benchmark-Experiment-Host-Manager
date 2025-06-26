## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 1119s 
    Code: 1750150367
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.8.
    Experiment is limited to DBMS ['PostgreSQL'].
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
    disk:399210064
    datadisk:5805
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750150367

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           PostgreSQL-BHT-8-1-1
TPC-DS Q1                    321.74
TPC-DS Q2                    854.14
TPC-DS Q3                    504.21
TPC-DS Q4                  15805.62
TPC-DS Q5                   1428.59
TPC-DS Q6                 218550.20
TPC-DS Q7                   1122.21
TPC-DS Q8                    146.75
TPC-DS Q9                   6133.30
TPC-DS Q10                  3109.86
TPC-DS Q11                 11850.95
TPC-DS Q12                   215.05
TPC-DS Q13                  1924.69
TPC-DS Q14a+b               7842.38
TPC-DS Q15                   344.82
TPC-DS Q16                   698.62
TPC-DS Q17                  1045.41
TPC-DS Q18                  1200.03
TPC-DS Q19                   487.97
TPC-DS Q20                   298.23
TPC-DS Q21                   693.68
TPC-DS Q22                 10040.65
TPC-DS Q23a+b              11247.33
TPC-DS Q24a+b                150.24
TPC-DS Q25                  1047.69
TPC-DS Q26                   755.48
TPC-DS Q27                   135.65
TPC-DS Q28                  4767.78
TPC-DS Q29                  1127.42
TPC-DS Q30                 29850.95
TPC-DS Q31                  6222.77
TPC-DS Q32                   236.63
TPC-DS Q33                  1141.41
TPC-DS Q34                    62.32
TPC-DS Q35                  3373.60
TPC-DS Q36                    59.33
TPC-DS Q37                   128.97
TPC-DS Q38                  3407.48
TPC-DS Q39a+b               7852.00
TPC-DS Q40                   346.34
TPC-DS Q41                  2049.37
TPC-DS Q42                   264.60
TPC-DS Q43                    61.84
TPC-DS Q44                  1369.90
TPC-DS Q45                   224.56
TPC-DS Q46                    59.90
TPC-DS Q47                  4255.90
TPC-DS Q48                  1845.05
TPC-DS Q49                  2153.64
TPC-DS Q50                   706.39
TPC-DS Q51                  2986.08
TPC-DS Q52                   261.93
TPC-DS Q53                   319.60
TPC-DS Q54                   203.32
TPC-DS Q55                   258.49
TPC-DS Q56                  1157.55
TPC-DS Q57                  2242.27
TPC-DS Q58                  1305.22
TPC-DS Q59                  1268.32
TPC-DS Q60                  1072.58
TPC-DS Q61                  4470.00
TPC-DS Q62                   296.18
TPC-DS Q63                   325.38
TPC-DS Q64                  2342.27
TPC-DS Q65                  1608.46
TPC-DS Q66                   623.51
TPC-DS Q67                  7069.65
TPC-DS Q68                    58.27
TPC-DS Q69                   717.44
TPC-DS Q70                  1226.45
TPC-DS Q71                   965.12
TPC-DS Q72                  2875.61
TPC-DS Q73                    62.40
TPC-DS Q74                  3730.10
TPC-DS Q75                  2373.77
TPC-DS Q76                   601.67
TPC-DS Q77                  5266.46
TPC-DS Q78                  3539.05
TPC-DS Q79                   503.51
TPC-DS Q80                  1472.34
TPC-DS Q81                125373.84
TPC-DS Q82                   926.16
TPC-DS Q83                   298.76
TPC-DS Q84                   256.94
TPC-DS Q85                   892.87
TPC-DS Q86                   484.80
TPC-DS Q87                  3366.65
TPC-DS Q88                  6745.89
TPC-DS Q89                   340.88
TPC-DS Q90                  2156.13
TPC-DS Q91                   422.71
TPC-DS Q92                  2174.54
TPC-DS Q93                   372.70
TPC-DS Q94                   460.10
TPC-DS Q95                  9591.05
TPC-DS Q96                   276.40
TPC-DS Q97                  1042.63
TPC-DS Q98                   500.53
TPC-DS Q99                   421.20

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0          130.0         1.0      145.0     284.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           1.07

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            3407.85

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-8-1 1.0 1              1                596      1  1.0           597.99

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
