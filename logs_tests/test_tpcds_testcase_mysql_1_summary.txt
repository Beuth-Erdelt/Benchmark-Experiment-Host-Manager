## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 601s 
    Code: 1750147336
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.8.
    Experiment is limited to DBMS ['MySQL'].
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
    disk:402001844
    datadisk:8290
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750147336

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MySQL-BHT-8-1-1
TPC-DS Q1                67.28
TPC-DS Q2                 6.49
TPC-DS Q3                 3.93
TPC-DS Q4                19.44
TPC-DS Q5                10.21
TPC-DS Q6                 2.38
TPC-DS Q7                 3.74
TPC-DS Q8                 6.24
TPC-DS Q9                11.52
TPC-DS Q10                4.36
TPC-DS Q11               13.61
TPC-DS Q12               14.36
TPC-DS Q13                4.22
TPC-DS Q14a+b            23.53
TPC-DS Q15                3.10
TPC-DS Q16                3.64
TPC-DS Q17                3.38
TPC-DS Q18                3.28
TPC-DS Q19                2.41
TPC-DS Q20                3.18
TPC-DS Q21                3.06
TPC-DS Q22                2.00
TPC-DS Q23a+b            14.69
TPC-DS Q24a+b             8.97
TPC-DS Q25                2.41
TPC-DS Q26                1.88
TPC-DS Q27                2.07
TPC-DS Q28                3.06
TPC-DS Q29                2.41
TPC-DS Q30                5.40
TPC-DS Q31                7.57
TPC-DS Q32                2.09
TPC-DS Q33                5.64
TPC-DS Q34                2.63
TPC-DS Q35                4.23
TPC-DS Q36                3.39
TPC-DS Q37                2.73
TPC-DS Q38                2.47
TPC-DS Q39a+b             8.10
TPC-DS Q40                2.64
TPC-DS Q41                2.59
TPC-DS Q42                1.90
TPC-DS Q43                4.58
TPC-DS Q44                2.88
TPC-DS Q45                2.01
TPC-DS Q46                3.19
TPC-DS Q47                5.24
TPC-DS Q48                2.86
TPC-DS Q49                5.08
TPC-DS Q50                2.74
TPC-DS Q51                3.97
TPC-DS Q52                1.92
TPC-DS Q53                2.34
TPC-DS Q54                7.39
TPC-DS Q55                1.74
TPC-DS Q56                4.29
TPC-DS Q57                5.33
TPC-DS Q58                5.16
TPC-DS Q59                4.09
TPC-DS Q60                4.22
TPC-DS Q61                2.47
TPC-DS Q62                2.91
TPC-DS Q63                2.20
TPC-DS Q64                6.29
TPC-DS Q65                2.05
TPC-DS Q66                5.30
TPC-DS Q67                1.85
TPC-DS Q68                1.85
TPC-DS Q69                2.24
TPC-DS Q70                2.30
TPC-DS Q71                2.58
TPC-DS Q72                2.94
TPC-DS Q73                3.00
TPC-DS Q74                4.59
TPC-DS Q75                4.39
TPC-DS Q76                2.44
TPC-DS Q77                6.21
TPC-DS Q78                3.78
TPC-DS Q79                2.16
TPC-DS Q80                4.10
TPC-DS Q81                2.79
TPC-DS Q82                1.88
TPC-DS Q83                5.09
TPC-DS Q84                2.17
TPC-DS Q85                2.54
TPC-DS Q86                2.05
TPC-DS Q87                2.04
TPC-DS Q88                4.63
TPC-DS Q89                1.89
TPC-DS Q90                1.44
TPC-DS Q91                1.81
TPC-DS Q92                1.65
TPC-DS Q93                2.70
TPC-DS Q94                2.14
TPC-DS Q95                2.56
TPC-DS Q96                2.17
TPC-DS Q97                3.99
TPC-DS Q98                2.18
TPC-DS Q99                2.26

### Loading [s]
                 timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MySQL-BHT-8-1-1           1.0           12.0         9.0      160.0     189.0

### Geometric Mean of Medians of Timer Run [s]
                 Geo Times [s]
DBMS                          
MySQL-BHT-8-1-1            0.0

### Power@Size ((3600*SF)/(geo times))
                 Power@Size [~Q/h]
DBMS                              
MySQL-BHT-8-1-1         1005866.59

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                             time [s]  count   SF  Throughput@Size
DBMS          SF  num_experiment num_client                                       
MySQL-BHT-8-1 1.0 1              1                 11      1  1.0          32400.0

### Workflow

#### Actual
DBMS MySQL-BHT-8 - Pods [[1]]

#### Planned
DBMS MySQL-BHT-8 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
